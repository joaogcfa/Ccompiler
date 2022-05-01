

{
    a = 0;
    b = 1;
    while ((a < 99999) && (b == 1))
    {
        a = a + 1;
        printf(a);
        if (a == 5)
        {
            b = 0;
        }
    }
    printf(a);
}
