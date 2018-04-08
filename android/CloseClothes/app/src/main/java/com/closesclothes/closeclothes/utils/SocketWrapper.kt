package com.closesclothes.closeclothes.utils


import android.util.Log
import com.closesclothes.closeclothes.MainActivity

import java.io.DataOutputStream
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.Socket

import org.json.JSONException
import org.json.JSONObject
import java.nio.ByteBuffer

class SocketWrapper {

    private var socket: Socket? = null

//    private val IP = "192.168.0.105" // server's ip
    private val IP = "192.168.0.108" // server's ip


    init {
        try {
            Log.i(MainActivity::TAG.toString(), "b4 socket connect")
            socket = Socket(IP, 8080)
            Log.i(MainActivity::TAG.toString(), "after socket connect")
        } catch (e: IOException) {
            e.printStackTrace()
        }

    }


    fun sendJson(json: JSONObject) {
        send(byteArrayOf(1))
        val jsonStr = json.toString()
        send(intToByteArray(jsonStr.length))
        send(jsonStr.toByteArray())
    }

    fun receiveJson(): JSONObject? {
        val numJsonBytes = receiveInt()
        val jsonStr = String(receive(numJsonBytes)!!)
        try {
            return JSONObject(jsonStr)
        } catch (e: JSONException) {
            e.printStackTrace()
            return null
        }

    }

    fun send(data: ByteArray) {
        val out: OutputStream
        try {
            out = socket!!.getOutputStream()
            val dos = DataOutputStream(out)
            dos.write(data, 0, data.size)
        } catch (e: IOException) {
            // TODO Auto-generated catch block
            e.printStackTrace()
        }

    }

    private fun receiveInt(): Int {
        val intbytes = receive(4)
        return ByteBuffer.wrap(intbytes).getInt()
    }

    private fun receive(len: Int): ByteArray? {
        var stream: InputStream? = null
        val data = ByteArray(len)
        try {
            stream = socket!!.getInputStream()
            val count = stream!!.read(data)
            if (count != len) {
                Log.i(MainActivity::TAG.toString(), "ERROR: didn't read all wanted bytes, read:$count bytes")
                return null
            }
            return data
        } catch (e: IOException) {
            e.printStackTrace()
        }

        return null
    }


     fun intToByteArray(a: Int): ByteArray {
        val ret = ByteArray(4)
        ret[3] = (a and 0xFF).toByte()
        ret[2] = (a shr 8 and 0xFF).toByte()
        ret[1] = (a shr 16 and 0xFF).toByte()
        ret[0] = (a shr 24 and 0xFF).toByte()
        return ret
    }

    fun closeSocket() {
        try {
            this.socket!!.close()
        } catch (e: IOException) {
            e.printStackTrace()
        }

    }

}
