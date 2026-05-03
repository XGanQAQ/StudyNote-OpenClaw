
[141. 环形链表 - 力扣（LeetCode）](https://leetcode.cn/problems/linked-list-cycle/description/)

```cs
public class Progrom
{
    public static void Main()
    {
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);

        // Create a cycle for testing
        head.next.next.next.next = head.next; // Creates a cycle

        Solution solution = new Solution();
        bool hasCycle = solution.HasCycle(head);

        Console.WriteLine("Does the linked list have a cycle? " + hasCycle);
    }
}
public class ListNode
{
    public int val;
    public ListNode next;
    public ListNode(int x)
    {
        val = x;
        next = null;
    }
}

public class Solution
{
    public bool HasCycle(ListNode head)
    {
        if (head == null || head.next == null)
        {
            return false;
        }

        ListNode slowPtr = head;
        ListNode fastPtr = head.next;
        while (slowPtr != fastPtr)
        {
            if (fastPtr == null || fastPtr.next == null)
            {
                return false;
            }

            slowPtr = slowPtr.next;
            fastPtr = fastPtr.next.next;
        }

        return true;
    }
}
```

#双指针 解法