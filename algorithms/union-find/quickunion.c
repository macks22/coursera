// Union-Find using the quick-union (lazy strategy).
// Find is O(n) because of worst case root lookup for tall, skinny trees.
// Union is O(n) for the same reason.

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

int uf_root(UnionFind *uf, int id) {
    /* Return the root of node n. */
    if (id >= uf->size) {
        printf("indices out of bounds in `uf_root`\n");
        exit(1);
    }
    while (id != uf->nodes[id]) {
        id = uf->nodes[id];
    }
}

void uf_union(UnionFind *uf, int n1, int n2) {
    /* Join the two nodes together.
     * This implementation is O(n).
     */
    int i, root1, root2;

    if (n1 >= uf->size || n2 >= uf->size) {
        return;
    }
    root1 = uf_root(uf, n1);
    root2 = uf_root(uf, n2);

    // change root of first to root of second
    uf->nodes[root1] = uf->nodes[root2];
}

int uf_find(UnionFind *uf, int n1, int n2) {
    /* Return 1 if the two nodes are connected, else 0.
     * This implementation is O(n).
     */
    if (n1 >= uf->size || n2 >= uf->size) {
        return 0;
    }
    return uf_root(uf, n1) == uf_root(uf, n2);
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

void test1 () {
    UnionFind *uf = uf_create(10);
    printf("start:  ");
    uf_print(uf);

    uf_union(uf, 1, 2);
    assert(uf_find(uf, 1, 2));
    printf("(1, 2): ");
    uf_print(uf);

    uf_union(uf, 3, 4);
    assert(uf_find(uf, 3, 4));
    printf("(3, 4): ");
    uf_print(uf);

    uf_union(uf, 8, 9);
    assert(uf_find(uf, 8, 9));
    printf("(8, 9): ");
    uf_print(uf);

    uf_union(uf, 1, 8);
    assert(uf_find(uf, 1, 8));
    assert(uf_find(uf, 2, 8));
    assert(uf_find(uf, 2, 9));
    assert(uf_find(uf, 9, 1));
    printf("(1, 8): ");
    uf_print(uf);

    printf("end:    ");
    uf_print(uf);
    uf_destroy(uf);
}

void test2 () {
    UnionFind *uf = uf_create(10);
    printf("start:  ");
    uf_print(uf);

    uf_union(uf, 4, 3);
    uf_union(uf, 3, 8);
    uf_union(uf, 6, 5);
    uf_union(uf, 9, 4);
    uf_union(uf, 2, 1);
    uf_union(uf, 5, 0);
    uf_union(uf, 7, 2);
    uf_union(uf, 6, 1);
    uf_union(uf, 7, 3);

    assert(uf->nodes[0] == 1);
    assert(uf->nodes[1] == 8);
    assert(uf->nodes[2] == 1);
    assert(uf->nodes[3] == 8);
    assert(uf->nodes[4] == 3);
    assert(uf->nodes[5] == 0);
    assert(uf->nodes[6] == 5);
    assert(uf->nodes[7] == 1);
    assert(uf->nodes[8] == 8);
    assert(uf->nodes[9] == 8);

    printf("end:    ");
    uf_print(uf);
    uf_destroy(uf);
}

int main () {
    printf("TEST 1.\n");
    test1();
    printf("\nTEST 2.\n");
    test2();
    return 0;
}
