#include <iostream>
using namespace std;

class Node {
public:
	int data;
	Node* left;
	Node* right;
};

class Tree {
private:
	Node* root;
	void recursive_insert(Node*& subroot, int n)
	{
		if(subroot == NULL)
		{
			subroot = new Node();
			subroot->data = n;
			subroot->left = NULL;
			subroot->right = NULL;
		}
		else
		{
			if(n < subroot->data)
				recursive_insert(subroot->left, n);
			else
				recursive_insert(subroot->right, n);
		}
	}
	
	void recursive_NLR(Node* subroot)
	{
		if(subroot != NULL)
		{
			cout << subroot->data << " ";
			recursive_NLR(subroot->left);
			recursive_NLR(subroot->right);
		}
	}
	
	void recursive_LNR(Node* subroot)
	{
		if(subroot != NULL)
		{
			recursive_LNR(subroot->left);	
			cout << subroot->data << " ";
			recursive_LNR(subroot->right);
		}
	}
	
	int recursive_height(Node* subroot)
	{
		if(subroot == NULL)
		{
			return 0;
		}
		else
		{
			int a = recursive_height(subroot->left);
			int b = recursive_height(subroot->right);
			
			if(a > b)
				return a + 1;
			else
				return b + 1;
		}
	}
	int recursive_countNode(Node* subroot)
	{
		if(subroot == NULL)
		{
			return 0;
		}
		else
		{
			int a = recursive_countNode(subroot->left);
			int b = recursive_countNode(subroot->right);
			
			return a + b + 1;
		}
	}
	
	int recursive_countLeaf(Node* subroot)
	{
		if(subroot == NULL)
		{
			return 0;
		}
		else
		{
			if(subroot->left == NULL && subroot->right == NULL)
				return 1;
			
			int a = recursive_countLeaf(subroot->left);
			int b = recursive_countLeaf(subroot->right);
			
			return a + b;
		}
	}
	
public:
	int height()
	{
		return recursive_height(root);
	}
	
	int countNode()
	{
		return recursive_countNode(root);
	}
	
	int countLeaf()
	{
		return recursive_countLeaf(root);
	}

	void printNLR()
	{
		recursive_NLR(root);
	}
	
	void printLNR()
	{
		recursive_LNR(root);
	}

	Tree()
	{
		root = NULL;
	}
	
	void insert(int n)
	{
		recursive_insert(root, n);
	}

};

int main()
{
	Tree t;
	t.insert(4);
	t.insert(2);
	t.insert(7);
	t.insert(1);
	//t.insert(6);
	t.insert(8);
	t.insert(9);
	cout << t.countLeaf();
}
