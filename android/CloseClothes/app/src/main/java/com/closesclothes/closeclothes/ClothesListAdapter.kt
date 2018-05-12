package com.closesclothes.closeclothes


import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.TextView
import com.closesclothes.closeclothes.R
import com.squareup.picasso.Picasso
import org.json.JSONObject

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
                                   var tv2: TextView?)

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

            viewHolder = ViewHolder(position, clotheImage, clotheTv1, clotheTv2)
            viewHolder.position = position

            convertViewToReturn!!.setTag(viewHolder)

        } else {
            viewHolder = convertViewToReturn!!.getTag() as ViewHolder
        }

        var currentItemJsonObject = JSONObject(this.data[position])
        var currentItemFirstPicUrl = currentItemJsonObject.getJSONArray("imgs").getString(0)
        //load pic with Picasso library
        Picasso.get().load(currentItemFirstPicUrl).into(viewHolder.clotheImage);

        viewHolder.tv1?.setText(currentItemJsonObject.getString("url"))
        viewHolder.tv2?.setText("tv2")


        viewHolder.position = position
        return convertViewToReturn
    }

}