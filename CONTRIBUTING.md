# CONTRIBUTTING

## How to rub the Docherfile Locally 

...

docker rub -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"

...