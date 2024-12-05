import androidx.privacysandbox.tools.core.generator.build

val retrofit = Retrofit.Builder()
    .baseUrl("YOUR_API_BASE_URL")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val musicApi = retrofit.create(MusicApi::class.java)