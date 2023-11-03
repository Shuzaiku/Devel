FROM continuumio/miniconda3:latest

RUN mkdir -p app

WORKDIR /app

RUN conda update -c defaults conda -y && \
    conda install -c esri arcgis && \
    pip install shapely && \
    pip install python-dotenv

COPY . .

# EXPOSE 9000

CMD [ "python", "gcd.py" ]