from database.DB_connect import DBConnect
from model.traccia import Traccia
from model.Album import Album
class DAO:
    @staticmethod
    def get_album(soglia):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id ,a.title ,SUM(t.milliseconds )as durata
                    FROM track t , album a 
                    WHERE t.album_id =a.id 
                    GROUP BY a.id
                    HAVING  durata/60000 > %s

 """

        cursor.execute(query,(soglia,))

        for row in cursor:
            result[row["id"]]=Album(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_id(soglia):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id 
                        FROM track t , album a 
                        WHERE t.album_id =a.id 
                        GROUP BY a.id
                        HAVING  SUM(t.milliseconds )/60000 >= %s

     """

        cursor.execute(query, (soglia,))

        for row in cursor:
            result.append(row['id'])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_tracce():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM track t """

        cursor.execute(query)

        for row in cursor:
            result[row['id']] = Traccia(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_p_t():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT pt.playlist_id ,pt.track_id 
                    FROM playlist_track pt 
                    """

        cursor.execute(query)

        for row in cursor:
            result.append((row['playlist_id'],row['track_id']))

        cursor.close()
        conn.close()
        return result