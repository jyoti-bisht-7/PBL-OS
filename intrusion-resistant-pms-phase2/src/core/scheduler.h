#ifndef SCHEDULER_H
#define SCHEDULER_H

#ifdef __cplusplus
extern "C" {
#endif

// schedule_next: selects next pid to run given arrays of pids, priorities, remaining times.
// Returns selected pid, or -1 if none available.
int schedule_next(const int* pids, const int* priorities, const int* remaining, int n);

#ifdef __cplusplus
}
#endif

#endif // SCHEDULER_H
