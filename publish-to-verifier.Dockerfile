FROM 42labs/pontis-publisher:latest

COPY publish-to-verifier.py ./publish-to-verifier.py
COPY ecvrf.py ./ecvrf.py
CMD python publish-to-verifier.py
