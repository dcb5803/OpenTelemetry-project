from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

app = FastAPI()

# OpenTelemetry setup
provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "basic-otel-app"}))
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
provider.add_span_processor(processor)

FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)

@app.get("/")
def read_root():
    return {"message": "Hello from OpenTelemetry FastAPI!"}
