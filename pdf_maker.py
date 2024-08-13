import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF

class YouTubeVideoSummarizer:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.prompt = """You are a YouTube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within 250 words. Please provide the summary of the text given here:  """

    def extract_transcript_details(self, video_id):
        try:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join(item["text"] for item in transcript_text)
            return transcript
        except Exception as e:
            raise e

    def extract_local_video_transcript(self, video_url):
        # Placeholder function to extract transcript from local videos
        # This needs to be replaced with actual implementation
        return "This is a placeholder transcript for local video."

    def generate_gemini_content(self, transcript_text):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(self.prompt + transcript_text)
        return response.text

    def summarize_video(self, video_link):
        video_id = None

        if "youtube.com" in video_link:
            if "v=" in video_link:
                video_id = video_link.split("v=")[1].split("&")[0]
            elif "youtu.be" in video_link:
                video_id = video_link.split("/")[-1]
        elif "127.0.0.1:5000/" in video_link:
            video_id = video_link.split("/")[-1]

        if video_id:
            transcript_text = self.extract_transcript_details(video_id)
        else:
            transcript_text = self.extract_local_video_transcript(video_link)

        if transcript_text:
            summary = self.generate_gemini_content(transcript_text)
            print("## Detailed Notes:")
            print(summary)
            self.save_summary_to_pdf(summary, "summary.pdf")
        else:
            print("Invalid YouTube URL")

    def save_summary_to_pdf(self, text, filename):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in text.splitlines():
            pdf.multi_cell(0, 10, line)

        pdf.output(filename)

if __name__ == "__main__":
    app.run(debug=True)
