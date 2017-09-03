from ctr import lr
import time
import sched


class AdsRankingServiceHandler:
    def __init__(self):
        self._model = lr.LR()

        # periodic training
        self._running = False
        self._schedule = sched.scheduler(time.time, time.sleep)
        self._interval = 3600
        self._event = None
        pass

    # get ranking score of an ad
    def ranking(self, ad_query):
        print "Got query: ", ad_query
        x = self._model.preprocessor().transform_x(ad_query)
        score = self._model.predict(x)
        return score

    # re-train the model
    def train(self):
        self._model.train()

    # periodic train
    def periodic(self, action, actionargs=()):
        if self._running:
            self._event = self._schedule.enter(self._interval, 1, self.periodic, (action, actionargs))
            action(*actionargs)

    # start periodic task
    def start(self):
        self._running = True
        self.periodic(self.train)
        self._schedule.run()

    # start periodic task
    def stop(self):
        self._running = False
        if self._schedule and self._event:
            self._schedule.cancel(self._event)
            print "Periodic task is cancelled."
