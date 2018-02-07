# takes commandline arguments [place] [host] [user] [password] [database] [table] IN THAT ORDER

import pymysql as mariadb
import speedtest
import datetime
import sys
def main():
    # gets the location this test was run at
    place = sys.argv[1]
    # gets the host info to record to
    my_host = sys.argv[2]
    my_user = sys.argv[3]
    my_pass = sys.argv[4]
    my_datb = sys.argv[5]
    my_tabl = sys.argv[6]
    # get the current time and date, then format it for mariadb's datetime type
    time = datetime.datetime.now()
    testTime = "\"" + str(time.year) + '-' + str(time.month) + '-' + str(time.day) + ' ' + str(time.hour) + ':' + str(
        time.minute) + ':' + str(time.second) + "\""

    # Initialize the database connection
    # IMPORTANT: CONNECTION INFO SUBJECT TO CHANGE
    try:
        mariadb_connection = mariadb.connect(host=my_host,
                                             user=my_user,
                                             password=my_pass,
                                             database=my_datb)
    except mariadb.err.OperationalError:
        print("ERROR - Database unaccessible")
        exit();
    cursor = mariadb_connection.cursor()

    # speedtest API
    # Use this to specify a specific server to test against
    servers = []

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()
    # no real need to generate a share link, but I left it here to avoid confusion
    # when checking code against the API
    # s.share()
    # store the results in a local dictionary (just easier to type)
    results_dict = s.results.dict()
    # print(results_dict) #DEBUG MESSAGE
    dbsend = "INSERT INTO {:s} (time, place, dwnspd, upspd, server) VALUES ({:s}, \"{:s}\", {:.2f}, {:.2f}, \"{:s}\");".format(str(my_tabl),
                                                                                                             str(testTime),
                                                                                                             str(place),
                                                                                                             (results_dict[
                                                                                                                  "download"] / 1000.0 / 1000.0),
                                                                                                             (results_dict[
                                                                                                                  "upload"] / 1000.0 / 1000.0),
                                                                                                             str(results_dict["server"]["sponsor"]))
    print(dbsend)  # let user know insert statement is being sent
    cursor.execute(dbsend)
    mariadb_connection.commit()

    cursor.close()
    mariadb_connection.close()

if __name__== "__main__":
    main()