### Author: Kilian Cavalotti <kilian@stanford.edu>, Brock Palen <brockp@mlds-networks.com>

class dstat_plugin(dstat):
    """
    Read and write throughput (in bytes) on per Lustre filesystem.
    """
    def __init__(self):
        self.nick = ('read', 'write')
        self.cols = 2

    def discover(self, *objlist):
        ret = []
        for fs in os.listdir('/proc/fs/lustre/llite'):
            name = fs.split("-")[0]
            ret.append(name)
        for item in objlist: ret.append(item)
        if not ret:
            raise Exception, "No suitable Lustre filesystem found to monitor"
        return ret

    def check(self):
        if not os.path.exists('/proc/fs/lustre/llite'):
            raise Exception, 'Lustre filesystem not found'

    def name(self):
        return [fs.split("-")[0] for fs in os.listdir('/proc/fs/lustre/llite')]

    def vars(self):
        return [fs for fs in os.listdir('/proc/fs/lustre/llite')]

    def extract(self):
        for fs in self.vars:
            for line in open(os.path.join('/proc/fs/lustre/llite', fs, 'stats')).readlines():
                l = line.split()
                if len(line) < 6: continue
                if l[0] == 'read_bytes':
                    read = long(l[6])
                if l[0] == 'write_bytes':
                    write = long(l[6])
            self.set2[fs] = (read, write)

            self.val[fs] = map(lambda x, y: (y - x) * 1.0 / elapsed, self.set1[fs], self.set2[fs])

            if step == op.delay:
                self.set1.update(self.set2)

# vim:ts=4:sw=4
