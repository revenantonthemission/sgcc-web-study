import { marked } from "marked";
import hljs from "highlight.js";
import { markedHighlight } from "marked-highlight";
import { browser } from "$app/environment";

// Singleton markdown parser to avoid multiple instances
class MarkdownParser {
    private static instance: MarkdownParser;
    private parser: typeof marked;
    private initialized = false;

    private constructor() {
        this.parser = marked;
        this.initParser();
    }

    public static getInstance(): MarkdownParser {
        if (!MarkdownParser.instance) {
            MarkdownParser.instance = new MarkdownParser();
        }
        return MarkdownParser.instance;
    }

    private initParser() {
        if (this.initialized) return;
        
        this.parser.use(markedHighlight({
            langPrefix: "hljs language-",
            highlight(code, lang) {
                const language = hljs.getLanguage(lang) ? lang : "plaintext";
                return hljs.highlight(code, { language }).value;
            }
        }));
        this.parser.use({ gfm: true, breaks: true });
        this.initialized = true;
    }

    public async parse(text: string): Promise<string> {
        let renderedText = await this.parser.parse(text);
        
        if (browser) {
            const { default: DOMPurify } = await import("dompurify");
            return DOMPurify.sanitize(renderedText);
        }
        
        return renderedText;
    }
}

export const markdownParser = MarkdownParser.getInstance();