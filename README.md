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


マルチスレッドサーバとクライアントのひな形です。また，その拡張の方向性として他のプログラムも置いておきます。
2018/11/29 時点で，python-3.5 上での全ての動作を確認済み。

本音を言うと、mouse trace の UI を作って、自分の普段の作業時間とか記録したいんですけど、
時間がないのですよねー（キーボードの記録も追加したり、そういう機能が欲しいですよね・・・）
サーバー形式にしたのは、部屋全体で管理する可能性があったからです。
コメントは振っていないのと、データベース化もしてないですが、参考程度に。
