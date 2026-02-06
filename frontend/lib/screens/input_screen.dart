import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chart_provider.dart';
import 'chart_screen.dart';

class InputScreen extends StatefulWidget {
  const InputScreen({super.key});
  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  DateTime _selectedDate = DateTime(2000, 1, 1, 12, 0); // Default
  // Hardcoded Lat/Lon for New Delhi (You can add text fields later)
  final TextEditingController _latCtrl = TextEditingController(text: "28.7041");
  final TextEditingController _lonCtrl = TextEditingController(text: "77.1025");

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Create Kundali")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ListTile(
              title: Text("Date & Time: ${_selectedDate.toString()}"),
              trailing: const Icon(Icons.calendar_today),
              onTap: () async {
                final d = await showDatePicker(context: context, 
                    initialDate: _selectedDate, firstDate: DateTime(1900), lastDate: DateTime(2100));
                if (d != null) {
                   // ignore: use_build_context_synchronously
                   final t = await showTimePicker(context: context, initialTime: TimeOfDay.fromDateTime(_selectedDate));
                   if (t != null) {
                     setState(() => _selectedDate = DateTime(d.year, d.month, d.day, t.hour, t.minute));
                   }
                }
              },
            ),
            TextField(controller: _latCtrl, decoration: const InputDecoration(labelText: "Latitude")),
            TextField(controller: _lonCtrl, decoration: const InputDecoration(labelText: "Longitude")),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final lat = double.tryParse(_latCtrl.text) ?? 0.0;
                final lon = double.tryParse(_lonCtrl.text) ?? 0.0;
                
                await Provider.of<ChartProvider>(context, listen: false)
                    .generateChart(_selectedDate, lat, lon);
                
                if (mounted) {
                  Navigator.push(context, MaterialPageRoute(builder: (_) => const ChartScreen()));
                }
              },
              child: const Text("Generate Chart"),
            )
          ],
        ),
      ),
    );
  }
}