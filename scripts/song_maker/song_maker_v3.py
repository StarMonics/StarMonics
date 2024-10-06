from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override

# Initialize the OpenAI API client
client = OpenAI(api_key='API_KEY')

# Create an assistant for song generation
assistant = client.beta.assistants.create(
    name="Song Composer",
    instructions="You are a music assistant capable of generating Hans Zimmer inspired songs using ABC notation. The song should evoke a sense of cosmic wonder, with low-pitch, symphonic instrumentation. Only output the ABC notation and the instruments used.",
    tools=[{"type": "code_interpreter"}],  # Assuming Song Maker is a tool you can integrate
    model="gpt-4o"  # Specify the model
)

# Create a conversation thread
thread = client.beta.threads.create()

# Send the initial message (prompt)
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="""
    Create a grandiose orchestral song inspired by the following prompt:
    'In the cosmic expanse, a nebula blooms,
    Swirls of gas and dust like a dream in hues.
    Golden cliffs rise, sculpted by stellar winds,
    Reaching into the void where eternity begins.'

    Style: Symphonic, in the style of Hans Zimmer.
    Tone Sequence: A - B - C# - G#
    Tempo: 91 BPM
    Pitch: Low-pitch, inspirational and exploratory.
    Output the song only in ABC notation with its respective instruments.
    Do not output nothing more than the song in ABC notation and its respective instrumets. Remove it if there is anything else.
    """
)

# Define an event handler to handle the response stream
class SongMakerEventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > {text}", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        if delta.value:
            print(delta.value, flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > Song generation in progress using {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'song_maker' and delta.song_maker.outputs:
            for output in delta.song_maker.outputs:
                if output.type == "abc_notation":
                    print(f"ABC Notation:\n{output.abc_notation}", flush=True)

# Stream the response using the event handler
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=SongMakerEventHandler(),
) as stream:
    stream.until_done()
