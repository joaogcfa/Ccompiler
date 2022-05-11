{
    int x, y;
    str z;
    x = 1;
    y = x || (1 == 1);
    z = "x: ";
    printf(x + y);
    printf(z.x);
    printf(x + z); /* ERROR */
}