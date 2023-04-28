from diagrams import Diagram, Edge, Cluster
from diagrams.onprem.client import User, Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import SimpleStorageServiceS3 as s3
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.oci.monitoring import Telemetry
from diagrams.custom import Custom

with Diagram("Stock_Analysis_Summarizer", show=False, direction='LR'):
    user = Users("users")
    audiofile = Custom("Porfolio Excel", "./excel.png")
    textfile = Custom("Text File", "./textfile.png")
    datastorage = s3("AWS S3")

    with Cluster("Application Instance"):

        with Cluster("Services"):
            openai = Custom("Chat GPT", "./chatgpt.png")  

        with Cluster("Applications"):
            userfacing = Custom("Streamlit", "./streamlit.png")

        with Cluster("Batch Processing"):
            airflow = Airflow("Airflow") 
            whisper = Custom("Whisper", "./whisper.jpg")      
    
    # Defining Edges
    user >> Edge(label = "Creates") >> audiofile
    user >> Edge(label = "Login to Dashboard") >> userfacing
    user >> Edge(label = "Upload MP3 File") >> userfacing

    userfacing << Edge(label = "Strors MP3 file on S3") << datastorage    
    userfacing << Edge(label = "Fetches MP3 file from S3") << datastorage
    userfacing >> Edge(label = "Fetches Text file from S3") >> datastorage
    
    
    userfacing >> Edge(label = "Event Processing") >> airflow
    userfacing >> Edge(label = "Processes MP3 File") >> whisper
    whisper >> Edge(label = "Processses MP3 File and Creates")  >> textfile
    textfile >> Edge(label = "Stored in S3") >> datastorage

    openai << Edge(label = "Uses Text File to Answer Adhoc Questions") << userfacing

    airflow >> Edge(label = "Stores Transcribed Files to S3 Bucket") >> datastorage

from diagrams import Diagram, Edge, Cluster
from diagrams.onprem.client import User, Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import SimpleStorageServiceS3 as s3
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.oci.monitoring import Telemetry
from diagrams.custom import Custom
from diagrams.oci.compute import VM

with Diagram("Stock_Analysis_Summarizer", show=False, direction='LR'):
    user = Users("users")
    # audiofile = Custom("Porfolio Excel", "excel.png")
    datastorage = s3("AWS S3")

    with Cluster("Application Instance Flow"):

        with Cluster("Applications"):
            userfacing = Custom("Streamlit", "streamlit.png")
            fastAPI = Custom("FAST API", "fastapi.png")

        with Cluster("Database"):
            snowflake = Custom("Snowflake", "snowflake.png")

        with Cluster("TickerInfo"):
            gpt = Custom("GPT", "gpt.png")

        with Cluster("Daily Article Fetcher"):
            airflow = Airflow("Airflow") 
            whisper = Custom("RapidAPI", "rapidapi.png")
            seekingAlpha = Custom("Seeking Alpha", "seekingalpha.png") 

        with Cluster("New Article Fetcher"):
            airflow1 = Airflow("Airflow") 
            whisper1 = Custom("RapidAPI", "rapidapi.png")
            seekingAlpha1 = Custom("Seeking Alpha", "seekingalpha.png") 

        with Cluster("Post DAG") as c2:
            huggingFace = Custom("Hugging Face", "huggingface.png")
            procusFinbert = Custom("ProsusAI/finbert", "procus.png")
            bertSummary = Custom("Summary BERT", "bert.png")

    
    # Defining Edges
    # user >> Edge(label = "Creates") >> audiofile
    user >> Edge(label = "SignUp/Login to Dashboard") >> userfacing
    # user >> audiofile
    # audiofile >> Edge(label = "Upload Stock Portfolio") >> userfacing  

    userfacing >> fastAPI 
    fastAPI - Edge(color="red", ltail="Applications", lhead="Daily Article Fetcher") - airflow
    fastAPI - Edge(color="red", ltail="Applications", lhead="New Article Fetcher") - airflow1

    userfacing >> Edge(label = "Gets ticker name based on Company")>> gpt
    fastAPI >> snowflake
    
    userfacing >> Edge(label = "Triggers on a daily basis") >> airflow 
    airflow >> Edge(label = "Fetches the top 10 NASDAQ stock tickers") >> whisper
    whisper << seekingAlpha
    whisper >> seekingAlpha

    airflow >> Edge(label = "Stores news summaries on S3") >> datastorage

    datastorage >> Edge(label = "Storing the Summarized Articles") >> userfacing

    seekingAlpha - Edge(color="red", ltail="Daily Article Fetcher", lhead="Post DAG") - huggingFace

    ##
    userfacing >> Edge(label = "Triggers if user ticker other than top 10 nasdaq ticker") >> airflow1 
    airflow1 >> Edge(label = "Fetches the new and summary for the new ticker") >> whisper1
    whisper1 << seekingAlpha1
    whisper1 >> seekingAlpha1

    airflow1 >> Edge(label = "Stores news summaries on S3") >> datastorage

    datastorage >> Edge(label = "Storing the Summarized Articles") >> userfacing

    seekingAlpha1 - Edge(color="red", ltail="New Article Fetcher", lhead="Post DAG") - huggingFace
    ##

    userfacing  >> huggingFace
    huggingFace >> Edge(label = "Sentiment Analysis")>> procusFinbert
    procusFinbert >> Edge(label = "Summarises all positive and all negative sentives in one positive/negative sentiment") >> bertSummary

    bertSummary >> Edge(label= "Stores summary int S3") >> datastorage
    
    # whisper >> Edge(label = "Processses MP3 File and Creates")  >> textfile
    textfile >> Edge(label = "Stores summaries in S3") >> datastorage

    openai << Edge(label = "Uses Text File to Answer Adhoc Questions") << userfacing