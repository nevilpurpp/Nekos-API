export default async function handler(req, res) {
    const r = await fetch('https://betteruptime.com/api/v2/monitors/1100535', {
        headers: {
            Authorization: `Bearer ${process.env.BETTER_UPTIME_TOKEN}`,
            Accept: `application/vnd.api+json`
        }
    })
    const json = await r.json()

    res.status(200).json({
        status: json.data.attributes.status
    })
}
