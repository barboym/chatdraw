
import psycopg2
import dotenv

dotenv.load_dotenv()




if __name__=="__main__":
    conn = psycopg2.connect("dbname=sketches user=myuser")
    cur = conn.cursor()
    cur.execute("SELECT sketch_id FROM sketches WHERE concept = giraffe")
    result = cur.fetchone()
    print(result)