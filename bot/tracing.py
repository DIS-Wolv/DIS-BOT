"""Jaeger tracing.

>>> import time
>>> with TRACER.start_as_current_span("test") as span:
>>>     print(span)
>>>     time.sleep(0.1)
>>>     with TRACER.start_as_current_span("sub") as sub:
>>>         time.sleep(0.1)
>>>         sub.add_event("log message")
>>>         time.sleep(0.1)
>>>     time.sleep(0.1)
>>>     with TRACER.start_as_current_span("sub 2") as sub:
>>>         time.sleep(0.1)
>>>         sub.add_event("log message 2")
>>>         time.sleep(0.1)
"""
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


resource = Resource(attributes={SERVICE_NAME: "disbot"})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)


TRACER = trace.get_tracer("disbot")
