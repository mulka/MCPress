MCPress

Journalist-written news, natively accessible live to LLMs.
A licensed API that gives your AI agents access to up-to-date, journalist-written news—without scraping.

Each journalist is attached to an organization, they can submit new articles. To submit the article they upload the link to their article. From this url, we extract the content, using firecrawl or jina.ai), then we use LLM to remove any unnecessary content that’s not part of the article and extract the author and the publish date. Then, an LLM extract a summary and keywords and assign a category. We embed the summary with text-embedding-3-small for search (Reduce noise at fetch time). Once the user verifies, the article is saved into supabase for future search via MCP and our search functions.

the idea here would be to build a system we are journalists and news media more generally can publish their articles our we would have an MCP server that would allow AI Regents to access this content more specifically we our our app take the content the news article please and save it to be natively accessible so many modern format but I'm not sure about this you have to figure that out and we would extract some keywords not provided summary and also we would embed this news articles or maybe just the summary so that it can be queried by using similarity search and embedding space like a sort of a rag but in addition to that we want to so so the goal here would be that we can query or database of new species and our systems stores this news articles so that it can be easily queryable so really such as which media is writing this piece the date the category et cetera and then we would provide access in the form of an API meaning in the form of MCP server API access and maybe the news article has an image we would save the image as well as well as the text when you're querying this news piece and the idea here is that news media would get remunerated by access I don't know if you've seen the latest news regarding stack overflow but since they've opened up their API they made more money than ever so the idea here would be to provide API access news content and one of the is for news media not to be get their news correct for free and the value for the agents is that they can get access to the latest news information through our API which has a search and it's more cost effective than scrapping things it's natively accessible.



Enables journalists to make money with their news articles.


Tech Stack

Frontend
NextJS
TypeScript


Python
FastAPI
FastMCP 3

Supabase
Supabase Auth
Organization email
