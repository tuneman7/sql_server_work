class Solution(object):
    def rotate(self, nums, k):
        """
        Do not return anything, modify nums in-place instead.
        """

        for shifts in range(k):
            #Get the last element
            l_e = nums[len(nums)-1]
            #rotate through the elements in backward order
            for i in range(len(nums)-1,-1,-1):
                #print(i)
                nums[i] = nums[i-1]

            #place the last element in place
            nums[0] = l_e

        print(nums)
        

nums = [1,2,3,4,5,6,7]
k = 3

ms = Solution()
ms.rotate(nums,k)

