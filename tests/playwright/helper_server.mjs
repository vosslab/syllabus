import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { once } from "node:events";

const CONTENT_TYPES = new Map([
	[".css", "text/css; charset=utf-8"],
	[".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
	[".html", "text/html; charset=utf-8"],
	[".js", "text/javascript; charset=utf-8"],
	[".json", "application/json; charset=utf-8"],
	[".pdf", "application/pdf"],
	[".svg", "image/svg+xml"],
	[".woff2", "font/woff2"],
]);

function resolveRequestPath(siteRoot, requestUrl) {
	const pathname = decodeURIComponent(new URL(requestUrl, "http://127.0.0.1").pathname);
	let targetPath = path.resolve(siteRoot, `.${pathname}`);
	if (!targetPath.startsWith(`${siteRoot}${path.sep}`) && targetPath !== siteRoot) {
		return null;
	}
	if (targetPath.endsWith(path.sep) || (fs.existsSync(targetPath) && fs.statSync(targetPath).isDirectory())) {
		targetPath = path.join(targetPath, "index.html");
	}
	return targetPath;
}

export async function startStaticServer(siteRoot) {
	const server = http.createServer((request, response) => {
		const targetPath = resolveRequestPath(siteRoot, request.url ?? "/");
		if (targetPath === null || !fs.existsSync(targetPath) || !fs.statSync(targetPath).isFile()) {
			response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
			response.end("Not found");
			return;
		}
		const contentType = CONTENT_TYPES.get(path.extname(targetPath)) ?? "application/octet-stream";
		response.writeHead(200, { "Content-Type": contentType });
		fs.createReadStream(targetPath).pipe(response);
	});
	server.listen(0, "127.0.0.1");
	await once(server, "listening");
	const address = server.address();
	if (typeof address === "string" || address === null) {
		throw new Error("Static test server did not receive a TCP port");
	}
	return {
		baseUrl: `http://127.0.0.1:${address.port}`,
		close: async () => {
			server.close();
			await once(server, "close");
		},
	};
}
