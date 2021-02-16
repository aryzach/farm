void crash_now(void)
{
    *((volatile uint32_t *)0) = 0; // null pointer deref, instant crash
}

void call_crash_now(void)
{
    for(int i = 0; i < 3; i++) {
        crash_now();
    }
}

void should_we_crash(bool crash_now)
{
    if(crash_now) {
        call_crash_now();
    }
}

void init_task(void *pvParameters)
{
    should_we_crash(true);
    while(1) { }
}
