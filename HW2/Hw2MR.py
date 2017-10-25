from mrjob.job import MRJob
from mrjob.step import MRStep
import statistics as stats

#Number of nodes in the graph
class MRNodes(MRJob):

    def mapper_get_nodes(self, _, line):
        li = line.strip()
        if not li.startswith("#"):
            nodes = li.split()
            yield nodes[0], 1
            yield nodes[1], 1

    def combiner_count_nodes(self, node, _):
        yield node, 1

    def reducer_count_nodes(self, word, _):
        yield "CountOfNode", 1

    def reducer_find_number_of_nodes(self, key, count):
        yield key, sum(count)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_nodes,
                   combiner=self.combiner_count_nodes,
                   reducer=self.reducer_count_nodes),
            MRStep(reducer=self.reducer_find_number_of_nodes)
        ]

#Average (and median) indegree
class MRIndegree(MRJob):

    def mapper_get_edges(self, _, line):
        li = line.strip()
        if not li.startswith("#"):
            edge = li.split()
            yield (edge[1], edge[0]), None

    def combiner_indegree(self, edge, _):
        yield edge, 1

    def reducer_indegree(self, edge, _):
        yield edge[0], 1
        yield edge[1], 0

    def reducer_count_indegree(self, node, count):
        yield "In", sum(count)

    def reducer_stat_indegree(self, _, values):
        val = []
        count = 0
        for i in values:
            if i > 100:
                count += 1
            val.append(i)

        #print(val)

        med = stats.median(val)
        avg = stats.mean(val)

        yield "Stats", (med, avg)
        yield "Num Nodes with Indegree greater than 100", count

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_edges,
                   combiner=self.combiner_indegree,
                   reducer=self.reducer_indegree),
            MRStep(reducer=self.reducer_count_indegree),
            MRStep(reducer=self.reducer_stat_indegree)
        ]


#Average (and median) out degree
class MROutdegree(MRJob):

    def mapper_get_edges(self, _, line):
        li = line.strip()
        if not li.startswith("#"):
            edge = li.split()
            yield (edge[0], edge[1]), None

    def combiner_edges(self, edge, _):
        yield edge, 1

    def reducer_edges(self, edge, _):
        yield edge[0], 1
        yield edge[1], 0

    def reducer_outdegree(self, node, count):
        yield "Out", sum(count)

    def reducer_stat_outdegree(self, _, values):
        val = []
        for i in values:
            val.append(i)

        med = stats.median(val)
        avg = stats.mean(val)
        #print(len(val))
        print(val)
        yield "Stats", (med, avg)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_edges,
                   combiner=self.combiner_edges,
                   reducer=self.reducer_edges),
            MRStep(reducer=self.reducer_outdegree),
            MRStep(reducer=self.reducer_stat_outdegree)
        ]


#Average (and median) number of nodes reachable in two hops
class MRTwoHops(MRJob):

    def mapper_1_hop(self, _, line):
        li = line.strip()
        if not li.startswith("#"):
            edge = li.split()
            yield edge[1], (edge[0], edge[1])
            yield edge[0], (edge[0], edge[1])

    def reducer_1_hop(self, node, edge):
        val = set()
        for i in edge:
            val.add(tuple(i))

        for i in val:
            if (node == i[1]):
                flag = 0
                for j in val:
                    if node == j[0]:
                        if(i[0] == node == j[1]):
                            continue
                        flag = 1
                        yield (i, j), 1

                if flag == 0:
                    yield (i[1], -1), 0


    def reducer_count_2_hops(self, edge, count):
        yield edge[0], sum(count)

    def reducer_count_edges(self, node, count):
        yield "Word", sum(count)

    def reducer_stat(self, _, values):
        val = []
        for i in values:
            val.append(i)

        med = stats.median(val)
        avg = stats.mean(val)
        print(val)
        yield "Stats", (med, avg)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_1_hop,
                   reducer=self.reducer_1_hop),
            MRStep(reducer=self.reducer_count_2_hops),
            MRStep(reducer=self.reducer_count_edges),
            MRStep(reducer=self.reducer_stat)
        ]


if __name__ == '__main__':
    #MRNodes.run()
    #MRIndegree.run()
    #MROutdegree.run()
    MRTwoHops.run()