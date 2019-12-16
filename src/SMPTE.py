class SMPTETimecode:
    def __init__(self, smpte_string):
        components = smpte_string.split(':')
        self.hour = components[0]
        self.minute = components[1]
        self.second = components[2]
        self.frame = components[3]

    def __gt__(self, other):
        if self.hour > other.hour:
            return True

        elif self.hour == other.hour:
            if self.minute > other.minute:
                return True

            elif self.minute == other.minute:
                if self.second > other.second:
                    return True

                elif self.second == other.second:
                    if self.frame > other.frame:
                        return True

                    else:
                        return False

                else:
                    return False

            else:
                return False
        else:
            return False

    def __ge__(self, other):
        if self.hour > other.hour:
            return True

        elif self.hour == other.hour:
            if self.minute > other.minute:
                return True

            elif self.minute == other.minute:
                if self.second > other.second:
                    return True

                elif self.second == other.second:
                    if self.frame >= other.frame:
                        return True

                    else:
                        return False

                else:
                    return False

            else:
                return False
        else:
            return False

    def __eq__(self, other):
        if self.hour == other.hour and self.minute == other.minute and\
             self.second == other.second and self.frame == other.frame:
            return True

        else:
            return False


class SMPTEInterval:
    def __init__(self, interval_string, sep=' '):
        times = interval_string.split(sep)
        self.init_time = SMPTETimecode(times[0])
        self.end_time = SMPTETimecode(times[1])

    def includes(self, smpte_timecode):
        if self.end_time >= smpte_timecode >= self.init_time:
            return True

        else:
            return False

    def overlaps(self, smpte_interval):
        if self.includes(smpte_interval.init_time):
            return True

        elif smpte_interval.includes(self.init_time):
            return True

        else:
            return False
