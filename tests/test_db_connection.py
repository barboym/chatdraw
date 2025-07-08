
import psycopg2
import dotenv

dotenv.load_dotenv()




if __name__=="__main__":
    conn = psycopg2.connect("dbname=sketchs user=myuser")
    cur = conn.cursor()
    cur.execute("SELECT sketch_data FROM sketches WHERE concept = %s", (concept,))
    result = cur.fetchone()