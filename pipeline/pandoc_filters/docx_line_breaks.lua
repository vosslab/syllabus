-- Translate the documented HTML break into a native Pandoc line break for DOCX.

function RawInline(raw_inline)
  -- ASVS 1.2.1 and 2.2.1: allow only the exact documented token at this output boundary.
  if raw_inline.format == "html" and raw_inline.text == "<br>" then
    return pandoc.LineBreak()
  end
  return nil
end
