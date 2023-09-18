# Description
- This is an application that can easily summarize your comments from specific uploaded YouTube videos and leverage natural language queries for efficient searches. Moreover, harness the power of the YouTube Analytics API v2 to extract insightful analytics data for both your individual uploaded videos and the entire channel.<br>
- Basically an improved version of **Youtube Studio** with a natural language querying feature over comments.
- **Note: You need to have a Youtube Channel with Videos uploaded.**
  
## Features
- **Comment Summarization:** Quickly generate summaries for comments associated with any YouTube video.
- **Natural Language Queries:** Use natural language queries to explore and search through comments seamlessly.
- **Analytics Insights:** Utilize the YouTube Analytics API v2 to retrieve valuable analytics data for videos and channels.


## Analytics Insights 
- **Views and Watch Time:** Information about the number of views and watch time for your videos and channel.
- **Likes and Dislikes:** The number of likes and dislikes on your videos.
- **Comments and Shares:** Viewer interactions through comments and shares on your content.
- **Subscribers and Subscriptions:** Growth of your subscriber base and subscription trends.

## Tools and Technologies used
- **Dash** - a Python web framework used for building interactive web applications.
- **Pandas** - efficiently managing and analyze the vast amounts of data associated with YouTube comments, providing insightful summaries.
- **Plotly** - crafting interactive data visualizations and charts.
- **Dash Bootstrap Components** - enhancing the visual appeal and functionality of the user interface.
- **OpenAI API** -  empowers users to effortlessly search, query, and summarize YouTube comments, making the application more intuitive and user-centric.
- **YouTube Analytics API v2** - extraction of comprehensive analytics data, including views, likes, comments, and more.
  

## Screenshots
![image](https://github.com/KevKibe/Content-Insight-Analytics/assets/86055894/cbf52212-7b0c-4d64-b0be-5c4e3b5ba69b)
![image](https://github.com/KevKibe/Content-Insight-Analytics/assets/86055894/0f752a2b-0c97-4836-acce-708357998b14)
![image](https://github.com/KevKibe/Content-Insight-Analytics/assets/86055894/bac63649-1b67-47f4-8007-9c64be261051)

## Installation and Usage 

- Clone the repository: `git clone https://github.com/KevKibe/YouTube-Comments-Insights-and-Analytics.git`
- Run this command on the console to install depenencies `pip install -r requirements.txt`
- Set up environment variables: Create a .env file in the root directory of the project and add your OpenAI API key and Youtube API Key as follows: `OPENAI_API_KEY=your_api_key_here` , `YT_API_KEY=your_api_key`
- Run the command `py dashboard.py` to spin up the server and you should see output indicating that the server is running. It will provide a local web address where you can access the dashboard (typically, http://127.0.0.1:8080/).
