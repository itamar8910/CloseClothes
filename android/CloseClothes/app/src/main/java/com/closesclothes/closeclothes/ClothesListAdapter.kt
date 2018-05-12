package com.closesclothes.closeclothes


import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.TextView
import com.squareup.picasso.Picasso
import org.json.JSONObject
import android.support.v4.content.ContextCompat.startActivity
import android.content.Intent



class ClothesListAdapter(context: Context, internal var layoutResourceId: Int, private val data: List<String>) : ArrayAdapter<String>(context, layoutResourceId, data) {
    private val tags: MutableList<String>

    init {
        tags = ArrayList()
        val size = data.size
        for (i in 0 until size) {
            tags.add("tag")
        }
    }

    internal data class ViewHolder(var position : Int,
                                   var clotheImage: ImageView?,
                                   var tv1: TextView?,
                                   var tv2: TextView?,
                                   var tv3: TextView?)

//    fun utf16ToUtf8(utf16Str : String) : String{
//
//    }

    fun unescapeUtf16(s: String): String {
        var i = 0
        val len = s.length
        var c: Char
        val sb = StringBuffer(len)
        while (i < len) {
            c = s[i++]
            if (c == '\\') {
                if (i < len) {
                    c = s[i++]
                    if (c == 'u') {
                        // TODO: check that 4 more chars exist and are all hex digits
                        c = Integer.parseInt(s.substring(i, i + 4), 16).toChar()
                        i += 4
                    } // add other cases here as desired...
                }
            } // fall through: \ escapes itself, quotes any character but u
            sb.append(c)
        }
        return sb.toString()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {

        // View rowView = convertView;
        val viewHolder: ViewHolder
        var convertViewToReturn : View? = convertView
        if (convertView == null) {
            val inflater = context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            convertViewToReturn = inflater.inflate(layoutResourceId,
             parent, false);

            var clotheImage = convertViewToReturn?.findViewById<ImageView>(R.id.clothes_lit_item_iv)
            var clotheTv1 = convertViewToReturn?.findViewById<TextView>(R.id.clothes_list_item_tv1)
            var clotheTv2 = convertViewToReturn?.findViewById<TextView>(R.id.clothes_list_item_tv2)
            var clotheTv3 = convertViewToReturn?.findViewById<TextView>(R.id.clothes_list_item_tv3)

            viewHolder = ViewHolder(position, clotheImage, clotheTv1, clotheTv2, clotheTv3)
            viewHolder.position = position

            convertViewToReturn!!.setTag(viewHolder)

        } else {
            viewHolder = convertViewToReturn!!.getTag() as ViewHolder
        }

        var currentItemJsonObject = JSONObject(this.data[position])
        var currentItemFirstPicUrl = currentItemJsonObject.getJSONArray("imgs").getString(0)
        //load pic with Picasso library
        Picasso.get().load(currentItemFirstPicUrl).into(viewHolder.clotheImage);

        viewHolder.tv1?.setText(this.unescapeUtf16(currentItemJsonObject.getString("name")))
        viewHolder.tv2?.setText(currentItemJsonObject.getString("price"))
        viewHolder.tv3?.setText(this.unescapeUtf16(currentItemJsonObject.getString("description")))



        viewHolder.position = position
        return convertViewToReturn
    }

}