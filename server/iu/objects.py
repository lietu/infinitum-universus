class GameObject(object):
    def update(self, time_elapsed):
        pass

    def get_sensor_data(self):
        raise NotImplementedError(
            "{} does not implement get_sensor_data()".format(
                self.__class__.__name__
            )
        )
