#include <iostream>
#include <vector>

void debugVector(std::vector<int> to_debug) {
    std::cout << "Debugging:" << std::endl;
    for (int i = 0; i < to_debug.size(); i++) {
        std::cout << std::to_string(to_debug[i]) + " ";
    }
    std::cout << "\n";
}

void mergeVector(std::vector<int> &into, std::vector<int> merging) {
    for (int i = 0; i < merging.size(); i++) {
        into.push_back(merging[i]);
    }
}

std::vector<int> quicksort(std::vector<int> unordered) {
    if (unordered.size() <= 1) return unordered;

    std::vector<int> small, big;
    int pivot = unordered.back();
    unordered.pop_back();

    for (int i = 0; i < unordered.size(); i++) {
        if (unordered[i] < pivot) {
            small.push_back(unordered[i]);
        }
        else {
            big.push_back(unordered[i]);
        }
    }

    std::vector<int> new_order;
    mergeVector(new_order, quicksort(small));
    new_order.push_back(pivot);
    mergeVector(new_order, quicksort(big));

    debugVector(new_order);

    return new_order;
}

int main() {
    std::vector<int> unordered {9, 3, 4, 1, 6, 3, 1};
    std::vector<int> ordered = quicksort(unordered);

    std::cout << "Sorted:" << std::endl;
    for (int i = 0; i < ordered.size(); i++) {
        std::cout << std::to_string(ordered[i]) + " ";
    }
    std::cout << "\n";

    return 0;
}
