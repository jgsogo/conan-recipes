#include <iostream>

#include "tree_composite.hpp"

namespace {

    struct NodeId {
        NodeId(std::string_view id) : id(id) {}

        const std::string id;
    };


    struct NodeIdNum {
        NodeIdNum(int idNum) : idNum(idNum) {}

        int idNum = 0;
        int depth = 0;
    };

    inline void onNodeAdded(const std::vector<std::reference_wrapper<NodeIdNum>> &gs, NodeIdNum &p) {
        p.depth = gs.size();
    }

    using IDTree = composite::Tree<NodeId>;
    using IDNumTree = composite::Tree<NodeIdNum>;
    using CompositeTree = composite::TreeCompose<IDTree, IDNumTree>::Tree;
}


int main()
{
    std::cout << "Test composite" << std::endl;

    auto root = std::make_shared<CompositeTree::TreeNode>("root", 0);
    auto node1 = std::make_shared<CompositeTree::TreeNode>("node1", 1);
    root->addChild(node1);

    auto node2 = std::make_shared<CompositeTree::TreeNode>("node2", 2);
    auto node3 = std::make_shared<CompositeTree::TreeNode>("node3", 3);
    node2->addChild(node3);
    root->addChild(node2);


    class Visitor : public CompositeTree::DFSVisitor {
    public:
        void visit(CompositeTree::NodeTypename &p) override {
            ids.push_back(p.id);
        }

    public:
        std::vector<std::string> ids;
    };
    Visitor visitor;
    visitor.start(*root);

    for (auto&& it: visitor.ids) {
        std::cout << it << std::endl;
    }
}
