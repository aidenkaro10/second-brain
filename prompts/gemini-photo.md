You are looking at a photo or screenshot that someone saved to their personal knowledge base. Extract everything useful from it. Output markdown with EXACTLY these sections, in this order:

# FRONTMATTER

```yaml
source: telegram photo
date_processed: (today's date)
kind: (screenshot of tweet / slide / whiteboard / textbook page / chart / other)
```

# TEXT IN IMAGE

Every word of text visible in the image, verbatim, in reading order. Keep formulas and numbers exact. If there is no text, write "No text."

# WHAT IT SHOWS

Plain-language description of what the image is: diagrams, charts, layouts, screenshots of which app, who is speaking if it's a post. 2-5 sentences.

# KEY TAKEAWAYS

3-5 bullets of what matters in this image for the stated purpose (given below). Base them only on what is actually in the image.

Constraints:
- Never invent text that is not legible. Mark unreadable parts as [illegible].
- Output markdown only, no preamble, no closing remarks.
