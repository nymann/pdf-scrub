# PDF Scrub

_Scrubs encrypted compressed PDF files for text watermarks and metadata._

1. Decrypts the PDF if it's encrypted
2. Uncompresses the PDF
3. Removes metadata (Xpacket)
4. Tries to naively remove text based watermarks by matching objects which number of occurrences, is the same as the PDF page count. If multiple objects match, produce a pdf for each.
5. Optionally compresses the PDF again if `--no-compress` is not given as a command line argument.

## Usage

```sh
$ pdf_scrub --help
Usage: pdf_scrub [OPTIONS] FILES...

Arguments:
  FILES...  [required]

Options:
  --compress / --no-compress      Compress the final pdf to reduce file size greatly  [default: compress]
```

## Dependencies

Requires `qpdf` and `pdftk`.

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
