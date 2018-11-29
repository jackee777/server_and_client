# server_and_client
This proglam is the sample server and clients and how to use it.
Simple_server is the basic model and the others are the extension of simple_server.

- simple_server
This has 2 components: multithread server and client.
These can easily reconnect; however it is difficult to shutdown the server.
I didn't write the situation that turn off the server.
(data_engineering server has the condition of the shutdown by the timer.)

- mouse_trace
It is extension of client to trace the mouse moving.
The purpose of this is the check of loging condition against users.
The future of this is to make the User Interface and to support User.
(Unfortunately, I don't have enough time to create it.)
The variable state_on is turn on or not and weight is the continuous time(bigger one is the long time you logged in).

- data_engineering
This has 3 components: dummy_device, quetionaire, and server.
The dummy_device is the alternative that you want to record the value. For example, mouse_trace.
The questionaire is the input of keyboard that I correspond to 4 values: good, bad, normal, reject.
The server is similar to the upper one; however it controlles the shutdown timing by another thread.
