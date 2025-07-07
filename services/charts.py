import plotly.graph_objects as go
import plotly.express as px
from services.vocab import get_vocab_status_count, get_vocab_count_last_7_days
from services.flashcard import get_flashcard_status_count

def plot_empty_donut(labels: list, colors: list, title="Chưa có dữ liệu"):
    # đếm số phần từ từ labels và tạo một danh sách values với các giá trị rất nhỏ
    values = [1e-6] * len(labels)  # số rất nhỏ để tạo lát mà không thấy
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            textinfo='none',
            hoverinfo="skip",
            marker=dict(colors=colors),
            opacity=0.3,  # làm mờ toàn bộ donut
            showlegend=True
        )
    ])
    
    fig.update_layout(
        title=title,
        margin=dict(t=50, b=20),
        height=300,
        legend=dict(
            font=dict(color="gray")  # làm mờ chú thích
        ),
        annotations=[dict(
            text="Chưa có<br>dữ liệu",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False,
            font_color="gray"
        )]
    )
    return fig

def plot_vocab_added_last_7_days(user_id: str):
    """
    Vẽ biểu đồ cột thể hiện số lượng từ vựng được thêm trong 7 ngày gần đây.
    
    Args:
        df (pd.DataFrame): DataFrame gồm 2 cột: 'date' (datetime), 'count' (int)
    
    Returns:
        plotly.graph_objects.Figure: Biểu đồ cột.
    """
    df = get_vocab_count_last_7_days(user_id=user_id)

    fig = go.Figure(data=[
        go.Bar(
            x=df["date"].apply(lambda x: x.strftime("%d/%m")),  # định dạng ngày tháng
            y=df["count"],
            #text=df["count"],  # hiển thị số trên đầu cột
            textposition='outside',
            marker_color="#3498db",
            hovertemplate="%{x} <br>Số từ: %{y}<extra></extra>"
        )
    ])
    fig.update_layout(
        title="Số lượng từ vựng mới trong 7 ngày gần đây",
        xaxis_title="Ngày",
        yaxis_title="Số từ",
        yaxis=dict(dtick=1),
        #xaxis=dict(tickangle=-45),  # xoay nhãn X để đỡ đè chữ
        plot_bgcolor='white',
        margin=dict(t=50, b=50, l=40, r=20),
        height=400
    )

    if sum(df["count"]) == 0:
        fig.add_annotation(
            text="Bạn chưa thêm từ mới nào trong 7 ngày gần đây.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray"),
            opacity=0.6
        )
    return fig

def plot_vocab_status_distribution(user_id: str):
    """
    Vẽ pie chart số lượng từ theo status từ DataFrame.
    """
    df = get_vocab_status_count(user_id=user_id)
    if df.empty:
        return plot_empty_donut(labels=["Đang học", "Đã nhớ"], colors=["#f39c12", "#2ecc71"], title="Tỉ lệ từ vựng theo trạng thái")

    fig = go.Figure(data=[
        go.Pie(
            labels=df["status"],
            values=df["count"],
            hole=0.6,
            textinfo='label+percent',
            insidetextorientation='radial',
            marker=dict(colors=["#f39c12", "#2ecc71"])
        )
    ])

    fig.update_layout(
        title="Tỉ lệ từ vựng theo trạng thái",
        margin=dict(t=50, b=20),
        height=300
    )
    return fig

def plot_flashcard_status_distribution(user_id: str):
    """
    Vẽ pie chart số lượng flashcard theo status từ DataFrame.
    """

    df = get_flashcard_status_count(user_id=user_id)
    if df.empty:
        return plot_empty_donut(labels=["Chưa làm", "Đã làm"], colors=["#e74c3c", "#8e44ad"], title="Tỉ lệ flashcard theo trạng thái")
    
    fig = go.Figure(data=[
        go.Pie(
            labels=df["status"],
            values=df["count"],
            hole=0.6,
            textinfo='label+percent',
            insidetextorientation='radial',
            marker=dict(colors=["#e74c3c", "#8e44ad"])
        )
    ])

    fig.update_layout(
        title="Tỉ lệ flashcard theo trạng thái",
        margin=dict(t=50, b=20),
        height=300
    )
    return fig

def plot_single_score_line(df):
    fig = px.line(
        df,
        x="time_updated",
        y="score",
        markers=True,
        labels={"time_updated": "Ngày làm bài", "score": "Điểm"},
        title="Tiến bộ điểm số theo thời gian"
    )
    fig.update_traces(
        hovertemplate="<br>".join([
            "Thời gian: %{x}",
            "Điểm: %{y}",
            "Flashcard: %{customdata[0]}"
        ]),
        customdata=df[["flashcard_name"]],
        marker=dict(size=9, line=dict(width=1, color='DarkSlateGrey'))
    )
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(automargin=True),
        height=400,
        margin=dict(t=50, b=40)
    )

    if df.empty:
        fig.update_layout(
            plot_bgcolor="rgba(240,240,240,0.3)",
        )
        fig.add_annotation(
            text="Bạn chưa làm flashcard nào.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray"),
        )
    return fig
