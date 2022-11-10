from .utils import extract_fnames
from ... import tests


class TigressUtilityTests(tests.UnitTestCase):
    def test_extract_fnames_comment1(self):
        """Tests that extract_fnames() does not matches single-line commented functions."""
        source = r"""//int foo() { }"""
        result = extract_fnames(source)
        self.assertEqual(result, [])

    def test_extract_fnames_comment2(self):
        """Tests that extract_fnames() does not matches multi-line commented functions."""
        source = r"""/*int addition(int arg1, int arg2)
{
    return arg1 + arg2;
}
*/"""
        result = extract_fnames(source)
        self.assertEqual(result, [])

    def test_extract_fnames_extern(self):
        """Tests that extract_fnames() does not matches extern functions."""
        source = r"""extern int foo();"""
        result = extract_fnames(source)
        self.assertEqual(result, [])

    def test_extract_fnames_fdeclaration(self):
        """Tests that extract_fnames() does not matches function declarations."""
        source = r"""void foo();"""
        result = extract_fnames(source)
        self.assertEqual(result, [])

    def test_extract_fnames_1(self):
        """Tests extract_fnames() with simple function."""
        source = r"""#include <stdio.h>
int addition(int arg1, int arg2)
{
     int sum;
     // Arguments are used here
     sum = arg1+arg2;

     /* Function return type is an integer. */
     return sum;
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["addition"])

    def test_extract_fnames_2(self):
        """Tests extract_fnames() with simple function."""
        source = r"""#include <stdio.h>
int addition(int arg1, int arg2){ int sum;

     // Arguments are used here
     sum = arg1+arg2;

     /* Function return type is an integer. */
     return sum;
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["addition"])

    def test_extract_fnames_3(self):
        """Tests extract_fnames() with more than one function."""
        source = r"""#include <stdio.h>
int
addition (int arg1, int arg2) {
     int sum;
     // Arguments are used here.
     sum = arg1+arg2;

     /* Function return type is an integer. */
     return sum;
}

int
subtraction (int arg1, int arg2){
    int sub;
    // Arguments are used here.
    sub = arg1-arg2;

    /*Function return type is an integer. */
    return sub;
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["addition", "subtraction"])

    def test_extract_fnames_4(self):
        """Tests extract_fnames() with functions returning a pointer."""
        source = r"""int * pointer()
{
    static int n = 1;
    return (&n);
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["pointer"])

    def test_extract_fnames_5(self):
        """Tests extract_fnames() on function with for loop."""
        source = r"""#include <stdio.h>

int main() {
    int i;

    for (i = 1; i < 11; ++i)
    {
        printf("%d ", i);
    }
    return 0;
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["main"])

    def test_extract_fnames_static(self):
        """Tests extract_fnames() with static function."""
        source = r"""static void
hello_world()
{
    puts("hello world!");
}"""
        result = extract_fnames(source)
        self.assertEqual(result, ["hello_world"])


class TigressTests(tests.UnitTestCase, tests.TransformTestCaseMixin):
    blueprint = "cmake-c"
    transform = "tigress"
