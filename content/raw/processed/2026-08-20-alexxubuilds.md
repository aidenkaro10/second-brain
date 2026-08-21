```yaml
source_url: https://www.tiktok.com/t/ZP8WK7jX9
platform: tiktok
creator: alexxubuilds
date_processed: 2026-08-20
```

# HOOK

- **Spoken words:** "let me show you how to give AI its own version of a search engine"
- **On-screen text:** "let me show you how to give AI its own version of a search engine"

# SCENE-BY-SCENE

- **00:00 - 00:03**: Medium close-up of creator holding a plush capybara microphone. Text overlay introduces the video concept. Fast cut transition.
- **00:03 - 00:13**: Series title banner appears ("the context bottleneck / 3. searching with RAG"). Graphics of database, book, and web icons pop up to illustrate prompt bloat.
- **00:14 - 00:21**: Flowchart showing user query to application, vector DB, and LLM appears on screen. Direct talking-head explanation.
- **00:22 - 00:35**: Mathematical vector graphics and 3D point cloud graphs overlay the video as high-dimensional vector embeddings are explained.
- **00:36 - 00:43**: 2D vector coordinate graph showing "Paris/France" vs "Berlin/Germany" relationship overlay.
- **00:44 - 00:55**: RAG indexing diagram appears showing text chunking, embedding models, and vector DB insertion.
- **00:56 - 01:05**: Query matching graphic displays how prompt embeddings compare to stored database chunks.
- **01:06 - 01:11**: Graphic of dot product vector formula overlay explaining similarity calculation.
- **01:12 - 01:16**: Return to talking head framing as creator wraps up benefits of RAG.

# FULL TRANSCRIPT

let me show you how to give AI its own version of a search engine. this is episode 3 in my series on the hidden bottleneck of LLMs: context. here's the problem. you can't just dump an entire database, textbook, or website into a prompt and expect the model to handle it perfectly. so instead, we give the model a way to search first and then answer. that's the basic idea behind RAG, or retrieval augmented generation. the first, arguably most important step to building RAG is turning your information into something that AI's can actually search through. it turns out that high dimensional vectors, or long lists of numbers, are surprisingly good at encoding meaning. specifically, we can embed data into these vectors so that chunks of text that have similar meaning have vector representations that are closer together, and vice versa. these embeddings not only encode distance, but also specific relationships. for example, the distance between the vectors for Paris and France and Berlin and Germany will look similar because that vector difference somehow encodes the idea of a capital city. now here's how these embeddings turn into a search engine. you take all the information you want the LLM to search through, split that information into smaller chunks, embed each chunk using some kind of embedding model, and take the resulting embedding vectors and store it in a specific database called a vector database. then when you send a prompt, the AI will embed that prompt too. it can compare your prompts with all the stored chunks and only pull back the ones closest in meaning simply by finding the vector representations that are closest to the embedding of your prompt. the easiest way to make this comparison is by simply taking the dot product between two vectors. the more positive, the more similar they are. now the model can be given just those most relevant pieces of information instead of cramming everything in.

# WHY IT WORKS

- **Compelling hook:** Promises a clear, high-value technical explanation within the first 3 seconds.
- **High visual density:** Frequent graphic and diagram overlays maintain visual interest and simplify abstract concepts.
- **Clear structure:** Breaks down complex AI architecture (RAG) into step-by-step sequential mechanics.
- **Relatable anchor:** Casual framing and plush toy prop make high-level technical subject matter approachable.