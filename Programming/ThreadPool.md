---
layout: programming
title: Thread Pool
---

## C++20 Thread Pool with work-stealing



An overloaded ```submit``` function with the return value deduced as a template parameter provides the required functionality for ```void``` and non-```void``` functions, with the latter returning a ```future```.

The ```requires``` feature separates the functions.

Both functions create A ```packaged_task``` out of the submitted function, and then load (a shared pointer of) the task into the job queue.
```cpp
// Submit a non-void function and returns the associated future
template <typename Func, typename... Args, typename Ret = std::invoke_result_t<std::decay_t<Func>, std::decay_t<Args>...>>
std::future<Ret> submit(Func&& f, Args&&... args) requires(!std::is_void<Ret>::value)
{
	auto task = std::make_shared<std::packaged_task<Ret()>>(std::bind(std::forward<Func>(f), std::forward<Args>(args)...));
	std::future<Ret> future = task->get_future();
	load(task);
	return future;
}

// Submits a void function
template <typename Func, typename... Args, typename Ret = std::invoke_result_t<std::decay_t<Func>, std::decay_t<Args>...>>
void submit(Func&& f, Args&&... args) requires(std::is_void<Ret>::value)
{
	auto task = std::make_shared<std::packaged_task<Ret()>>(std::bind(std::forward<Func>(f), std::forward<Args>(args)...));
	load(task);
}
```

The ```load``` function adds the function into one of the local work queues, and releases the corresponding semaphore so the task executes.

```cpp
template <typename Task>
void load(Task&& task) //Puts packaged task into work_load
{
	std::size_t qID = count++ % work_load.size(); //Gets index of work_deque least recently executed on
    jobs_left.fetch_add(1, std::memory_order::relaxed); //Adds 1 to the work_left counter
	work_load[qID].work.emplace([task]() { (*task)(); }); //Adds the function to the queue
	work_load[qID].sem.release(); //Increment semaphore so task can execute
}
```