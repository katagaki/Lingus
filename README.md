# Lingus

Converts Microsoft Office files into Markdown.

Uses LibreOffice for conversion to PDF, 
then uses Docling for conversion to Markdown.

## Running

1. Build the Docker image.

```zsh
docker build -t lingus .
```

2. Drop your files into the `docs` folder.

3. Create and run a new Docker container.

```zsh
docker run -v $(pwd)/docs:/app/docs -v $(pwd)/outputs:/app/outputs lingus
```

## Notes

- Docling is configured to only use the CPU. 
  To use the GPU, install the appropriate variant of PyTorch (good luck),
  then attach your GPU to the Docker container.
- No file type checks are currently being performed,
  which may result in non-Microsoft Office files and 
  hidden system files being picked up.