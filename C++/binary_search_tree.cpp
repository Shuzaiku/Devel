#include <iostream>
#include <vector>

struct BinarySearchTreeNode {
    int data;
    BinarySearchTreeNode *left = NULL, *right = NULL;

    BinarySearchTreeNode() {}
    BinarySearchTreeNode(int data) {
        this ->data = data;
    }

    void addChild(int child_data);

    std::vector<int> getInOrderTraversal() {
        std::vector<int> ordered_data;

        // left
        if (left != NULL) {
            std::vector<int> left_data = left->getInOrderTraversal();
            ordered_data.insert(ordered_data.end(), left_data.begin(), left_data.end());
        }

        // centre
        ordered_data.push_back(data);

        // right
        if (right != NULL) {
            std::vector<int> right_data = right->getInOrderTraversal();
            ordered_data.insert(ordered_data.end(), right_data.begin(), right_data.end());
        }

        return ordered_data;
    }

    bool search(int val) {
        // centre
        if (data == val) {
            return true;
        }

        // left
        if (val < data && left != NULL) {
            return left->search(val);
        } else {
            return false;
        }

        // right
        if (val > data && right != NULL) {
            return right->search(val);
        }
        return false;
    }
};

void BinarySearchTreeNode::addChild(int child_data) {
    if (child_data < data) { // left
        if (left != NULL) {
            left->addChild(child_data);
        }
        else {
            left = new BinarySearchTreeNode(child_data);
        }
    }
    else if (child_data > data) { // right
        if (right != NULL) {
            right->addChild(child_data);
        } else {
            right = new BinarySearchTreeNode(child_data);
        }
    }
}

BinarySearchTreeNode getTree(std::vector<int> v) {
    BinarySearchTreeNode node = BinarySearchTreeNode(v[0]);
    for (int i = 1; i < v.size(); i++) {
        node.addChild(v[i]);
    }
    return node;
}

int main()
{
    std::vector<int> unordered_vector = {19, 9, 8, 3, 17, 20, 6, 1, 5, 14};
    BinarySearchTreeNode node = getTree(unordered_vector);
    std::vector<int> ordered_vector = node.getInOrderTraversal();
    for (int i = 0; i < ordered_vector.size(); i++) {
        std::cout << ordered_vector[i] << std::endl;
    }
    return 0;
}