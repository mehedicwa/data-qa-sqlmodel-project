from sqlmodel import text
from apps.database import get_session


hotel_id = "b80acf46-4456-4972-a575-1709f4ee7d1a"


query = text(
    """
    SELECT
        TO_CHAR(DATE_TRUNC('month', st.date), 'YYYY-MM') AS month,
        s.name AS source_name,
        SUM(st.revenue) AS total_revenue
    FROM public.source_traffic st
    JOIN public.source s ON st.source_id = s.id
    JOIN public.hotel h ON st.hotel_id = h.id
    WHERE h.is_active = true
      AND st.hotel_id = :hotel_id
      AND st.date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '6 month'
      AND st.date < DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY month, s.name
    ORDER BY month, s.name;
    """
)


def get_last_6_months_source_revenue_by_hotel(hotel_id: str):
    with get_session() as session:
        result = session.execute(query, {"hotel_id": hotel_id}).fetchall()
        return result


source_revenue_data_by_hotel = get_last_6_months_source_revenue_by_hotel(hotel_id)

if source_revenue_data_by_hotel:
    print("Last 6 Months Revenue by Source:\n")
    for row in source_revenue_data_by_hotel:
        print(
            f"Month: {row.month}, Source: {row.source_name}, Revenue: {row.total_revenue}"
        )
else:
    print("No source revenue data found for the last 6 months.")
