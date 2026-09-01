-- Translate portable document-image metadata into Pandoc's DOCX width attribute.

local allowed_units = {
  cm = true,
  ["in"] = true,
  mm = true,
  pt = true,
}

function Image(image)
  local width = image.attributes["data-document-width"]
  if width == nil then
    return image
  end

  local number, unit = width:match("^(%d+%.?%d*)(%a+)$")
  if number == nil or tonumber(number) <= 0 or not allowed_units[unit] then
    error("data-document-width must be a positive number using in, cm, mm, or pt")
  end

  image.attributes.width = width
  image.attributes["data-document-width"] = nil
  return image
end
