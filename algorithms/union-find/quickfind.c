// Union-Find using the quick-find strategy (eager).
// Find is O(1), because it involves one comparison.
// Union is O(n), because it may involve up to n-1 assignments.

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>


typedef struct {
    int *nodes;
    int size;
} UnionFind;

UnionFind * uf_create(int size) {
    /* Create a new UnionFind struct */
    int i;
    UnionFind *uf = calloc(1, sizeof(UnionFind));
    uf->nodes = calloc(size, sizeof(int));
    uf->size = size;

    // initialize all node ids to their indices
    for (i = 0; i < size; i++) {
        uf->nodes[i] = i;
    }
    return uf;
}

void uf_destroy(UnionFind *uf) {
    /* Free up all memory for the UnionFind data structure. */
    free(uf->nodes);
    free(uf);
}

void uf_union(UnionFind *uf, int n1, int n2) {
    /* Join the two nodes together.
     * This implementation is O(n).
     */
    int i, id1, id2;

    if (n1 > uf->size || n2 > uf->size) {
        return;
    }
    id1 = uf->nodes[n1];
    id2 = uf->nodes[n2];

    // change all ids of the second to the id of the first
    for (i = 0; i < uf->size; i++) {
        if (uf->nodes[i] == id2) {
            uf->nodes[i] = id1;
        }
    }
}

int uf_find(UnionFind *uf, int n1, int n2) {
    /* Return 1 if the two nodes are connected, else 0.
     * This implementation is O(1).
     */
    if (n1 > uf->size || n2 > uf->size) {  // indices out of bounds
        return 0;
    }
    return uf->nodes[n1] == uf->nodes[n2];
}

void uf_print(UnionFind *uf) {
    /* Print out the nodes of the UnionFind data structure. */
    int i;
    for (i = 0; i < uf->size; i++) {
        printf("%d", uf->nodes[i]);
        if (i < uf->size-1) {
            printf(" ");
        }
    }
    printf("\n");
}

int main () {
    UnionFind *uf = uf_create(10);

    uf_union(uf, 1, 2);
    assert(uf->nodes[2] == uf->nodes[1]);
    assert(uf_find(uf, 1, 2));

    uf_union(uf, 3, 4);
    assert(uf->nodes[3] == uf->nodes[4]);
    assert(uf_find(uf, 3, 4));

    uf_union(uf, 8, 9);
    assert(uf->nodes[8] == uf->nodes[9]);
    assert(uf_find(uf, 8, 9));

    uf_union(uf, 1, 8);
    assert(uf->nodes[1] == uf->nodes[8]);
    assert(uf_find(uf, 1, 8));
    assert(uf_find(uf, 2, 8));
    assert(uf_find(uf, 2, 9));
    assert(uf_find(uf, 9, 1));

    uf_print(uf);
    uf_destroy(uf);
    return 0;
}
