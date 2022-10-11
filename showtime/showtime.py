import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

## Showtime GRPC Service
class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        """
            Load database
        """
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def GetScheduleByDate(self, request, context):
        """
            Get schedule of a specific date
        """
        for schedule in self.db:
            if schedule["date"] == request.date:
                print("Schedule Found!")
                return showtime_pb2.ScheduleData(date=schedule["date"], movies=schedule["movies"])
        return showtime_pb2.ScheduleData(date="", movies=[])

    def GetSchedule(self, request, context):
        """
            Get all schedules
        """
        for schedule in self.db:
            yield showtime_pb2.ScheduleData(date=schedule["date"], movies=schedule["movies"])  

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
