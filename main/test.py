import cohere  # Import Cohere library

# Initialize the Cohere client with your API key
cohere_client = cohere.Client('FoNuape43t1JZg1FBlLka3hERTlOq5SwjaSML3QX')  # Replace with your actual API key

# List all available models
models = cohere_client.models.list()

# Print out the available models
for model in models:
    print(model)
