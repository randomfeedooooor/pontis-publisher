FROM 42labs/pontis-publisher:latest

COPY publish-to-pontis.py ./publish-to-pontis.py
CMD python publish-to-pontis.py
