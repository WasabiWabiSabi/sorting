#!/bin/python3
'''
Python provides built-in sort/sorted functions that use timsort internally.
You cannot use these built-in functions anywhere in this file.

Every function in this file takes a comparator `cmp` as input
which controls how the elements of the
list should be compared against each other:
If cmp(a, b) returns -1, then a < b;
if cmp(a, b) returns  1, then a > b;
if cmp(a, b) returns  0, then a == b.
'''

import random
import copy


def cmp_standard(a, b):
    '''
    used for sorting from lowest to highest

    >>> cmp_standard(125, 322)
    -1
    >>> cmp_standard(523, 322)
    1
    '''
    if a < b:
        return -1
    if b < a:
        return 1
    return 0


def cmp_reverse(a, b):
    '''
    used for sorting from highest to lowest
    >>> cmp_reverse(125, 322)
    1
    >>> cmp_reverse(523, 322)
    -1
    '''
    if a < b:
        return 1
    if b < a:
        return -1
    return 0


def cmp_last_digit(a, b):
    '''
    used for sorting based on the last digit only

    >>> cmp_last_digit(125, 322)
    1
    >>> cmp_last_digit(523, 322)
    1
    '''
    return cmp_standard(a % 10, b % 10)


def _merged(xs, ys, cmp=cmp_standard):
    '''
    Assumes that both xs and ys are sorted,
    and returns a new list containing the elements of both xs and ys.
    Runs in linear time.

    NOTE:
    In python, helper functions are frequently
    prepended with the _.
    This is a signal to users of a library
    that these functions are for "internal use only",
    and not part of the "public interface".

    This _merged function could be implemented as a local function
    within the merge_sorted scope rather than a global function.
    The downside of this is that
    the function can then not be tested on its own.
    Typically, you should only implement a
    function as a local function if it cannot function on its own
    (like the go functions from binary search).
    If it's possible to make a function stand-alone,
    then you probably should
    do that and write test cases for the stand-alone function.

    >>> _merged([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    '''
# flags and empty list
    x = 0
    y = 0
    merged = []

# main loop
    while x < len(xs) and y < len(ys):
        cmp_value = cmp(xs[x], ys[y])

# if values are equal
        if cmp_value == 0:
            merged.append(xs[x])
            merged.append(ys[y])
            x += 1
            y += 1

# if xs value is larger than ys value
        if cmp_value == 1:
            merged.append(ys[y])
            y += 1

# if ys value is larger than xs value
        if cmp_value == -1:
            merged.append(xs[x])
            x += 1

# check if there are any remaining/trailing values in xs or ys
    while y < len(ys):
        merged.append(ys[y])
        y += 1
    while x < len(xs):
        merged.append(xs[x])
        x += 1

    return merged


def merge_sorted(xs, cmp=cmp_standard):
    '''
    Merge sort is the standard O(n log n) sorting algorithm.
    Recall that the merge sort pseudo code is:

        if xs has 1 element
            it is sorted, so return xs
        else
            divide the list into two halves left,right
            sort the left
            sort the right
            merge the two sorted halves

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    new_xs = copy.deepcopy(xs)
# base case
    if len(new_xs) == 1:
        return new_xs
    if len(new_xs) == 0:
        return new_xs
# recursive loop
    else:
        half_point = len(new_xs) // 2
        sorted_left = merge_sorted(new_xs[:half_point], cmp)
        sorted_right = merge_sorted(new_xs[half_point:], cmp)
        return _merged(sorted_left, sorted_right, cmp)


def quick_sorted(xs, cmp=cmp_standard):
    '''
    Quicksort is like mergesort,
    but it uses a different strategy to split the list.
    Instead of splitting the list down the middle,
    a "pivot" value is randomly selected,
    and the list is split into a "less than"
    sublist and a "greater than" sublist.

    The pseudocode is:

        if xs has 1 element
            it is sorted, so return xs
        else
            select a pivot value p
            put all the values less than p in a list
            put all the values greater than p in a list
            put all the values equal to p in a list
            sort the greater/less than lists recursively
            return the concatenation of (less than, equal, greater than)

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    new_xs = copy.deepcopy(xs)
    # base cases
    if len(new_xs) == 1:
        return new_xs
    if len(new_xs) == 0:
        return new_xs
    else:
        p = random.randrange(len(new_xs))
        less_than = []
        greater_than = []
        equal_to = []
        for x in new_xs:
            cmp_value = cmp(x, new_xs[p])
            if cmp_value == 0:
                equal_to.append(x)
            if cmp_value == 1:
                greater_than.append(x)
            if cmp_value == -1:
                less_than.append(x)
        return quick_sorted(less_than, cmp) + equal_to + \
            quick_sorted(greater_than, cmp)


def quick_sort(xs, cmp=cmp_standard):
    '''
    EXTRA CREDIT:
    The main advantage of quick_sort
    is that it can be implemented "in-place".
    This means that no extra lists are allocated,
    or that the algorithm uses Theta(1) additional memory.
    Merge sort, on the other hand,
    must allocate intermediate lists for the merge step,
    and has a Theta(n) memory requirement.
    Even though quick sort and merge
    sort both have the same Theta(n log n) runtime,
    this more efficient memory usage
    typically makes quick sort faster in practice.
    (We say quick sort has a lower "constant factor" in its runtime.)
    The downside of implementing quick sort in this way is
    that it will no longer be a [stable sort]
    (https://en.wikipedia.org/wiki/Sorting_algorithm#Stability),
    but this is typically inconsequential.

    Follow the pseudocode of the Lomuto partition scheme given on wikipedia
    (https://en.wikipedia.org/wiki/Quicksort#Algorithm)
    to implement quick_sort as an in-place algorithm.
    You should directly modify the input xs
    variable instead of returning a copy of the list.
    algorithm quicksort(A, lo, hi) is
    if lo < hi then
        p := partition(A, lo, hi)
        quicksort(A, lo, p - 1)
        quicksort(A, p + 1, hi)

    algorithm partition(A, lo, hi) is
    pivot := A[hi]
    i := lo
    for j := lo to hi do
        if A[j] < pivot then
            swap A[i] with A[j]
            i := i + 1
    swap A[i] with A[hi]
    return i
    '''
    if len(xs) == 0:
        return xs

    def quicksort(xs, lo, hi, cmp):
        if lo < hi:
            p = partition(xs, lo, hi, cmp)
            quicksort(xs, lo, p - 1, cmp)
            quicksort(xs, p + 1, hi, cmp)

    def partition(xs, lo, hi, cmp):
        p = xs[hi]
        i = lo
        for j in range(lo, hi + 1):
            if cmp(xs[j], p) == -1:
                swap = xs[i]
                xs[i] = xs[j]
                xs[j] = swap
                i += 1
        swap = xs[i]
        xs[i] = xs[hi]
        xs[hi] = swap
        return i

    return quicksort(xs, 0, len(xs) - 1, cmp)
