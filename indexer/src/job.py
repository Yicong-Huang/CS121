class Job:
    # Todo: add state related functions to job
    def __init__(self, path, url):
        self.path = path
        self.url = url

    def __str__(self):
        return 'job:%s:%s' % (self.path, self.url)

    @staticmethod
    def bytes_to_job(job_bytes):
        j = Job.decode(job_bytes).lstrip("job:")
        c = j.index(':')
        return Job(j[:c], j[c + 1:])

    @staticmethod
    def decode(s):
        return s.decode('utf-8')
